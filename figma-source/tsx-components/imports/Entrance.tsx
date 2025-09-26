import imgBafcd5E96F294A5FA58ADcf3Eeab8C901 from "figma:asset/2315ba0bc3061c3bfbe38c0bd1128cb3f578561c.png";

function HomeIndicator() {
  return <div className="absolute bottom-0 h-[34px] translate-x-[-50%] w-[375px]" data-name="Home Indicator" style={{ left: "calc(50% - 0.5px)" }} />;
}

function Button() {
  return (
    <div className="absolute bg-black box-border content-stretch flex gap-[8px] items-center justify-center px-[24px] py-[14px] rounded-[8px] shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] top-[12px] translate-x-[-50%] w-[343px]" data-name="Button" style={{ left: "calc(50% - 0.5px)" }}>
      <div className="flex flex-col font-['Inter:Medium',_'Noto_Sans_KR:Medium',_sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[16px] text-nowrap text-white">
        <p className="leading-[1.5] whitespace-pre">로그인</p>
      </div>
    </div>
  );
}

function BottomButton() {
  return (
    <div className="absolute bg-white bottom-[285px] h-[72px] translate-x-[-50%] w-[248px]" data-name="Bottom button" style={{ left: "calc(50% + 1.5px)" }}>
      <div className="h-[72px] overflow-clip relative w-[248px]">
        <HomeIndicator />
        {[...Array(3).keys()].map((_, i) => (
          <Button key={i} />
        ))}
      </div>
      <div aria-hidden="true" className="absolute border-[#e6e6e6] border-[0.5px_0px_0px] border-solid inset-0 pointer-events-none" />
    </div>
  );
}

function HomeIndicator1() {
  return <div className="absolute bottom-0 h-[34px] translate-x-[-50%] w-[375px]" data-name="Home Indicator" style={{ left: "calc(50% - 0.5px)" }} />;
}

function Button3() {
  return (
    <div className="absolute bg-black box-border content-stretch flex gap-[8px] items-center justify-center px-[24px] py-[14px] rounded-[8px] shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] top-[12px] translate-x-[-50%] w-[343px]" data-name="Button" style={{ left: "calc(50% - 0.5px)" }}>
      <div className="flex flex-col font-['Inter:Medium',_'Noto_Sans_KR:Medium',_sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[16px] text-nowrap text-white">
        <p className="leading-[1.5] whitespace-pre">로그인</p>
      </div>
    </div>
  );
}

function Button5() {
  return (
    <div className="absolute bg-black box-border content-stretch flex gap-[8px] items-center justify-center px-[24px] py-[14px] rounded-[8px] shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)] top-[12px] translate-x-[-50%] w-[343px]" data-name="Button" style={{ left: "calc(50% - 0.5px)" }}>
      <div className="flex flex-col font-['Inter:Medium',_'Noto_Sans_KR:Medium',_sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[16px] text-nowrap text-white">
        <p className="leading-[1.5] whitespace-pre">회원 가입</p>
      </div>
    </div>
  );
}

function BottomButton1() {
  return (
    <div className="absolute bg-white bottom-[215px] h-[70px] translate-x-[-50%] w-[248px]" data-name="Bottom button" style={{ left: "calc(50% - 1.5px)" }}>
      <div className="h-[70px] overflow-clip relative w-[248px]">
        <HomeIndicator1 />
        {[...Array(2).keys()].map((_, i) => (
          <Button3 key={i} />
        ))}
        <Button5 />
      </div>
      <div aria-hidden="true" className="absolute border-[#e6e6e6] border-[0.5px_0px_0px] border-solid inset-0 pointer-events-none" />
    </div>
  );
}

export default function Enterance() {
  return (
    <div className="bg-white relative size-full" data-name="enterance">
      <div className="absolute font-['Inter:Bold_Italic',_sans-serif] font-bold h-[61px] italic leading-[0] left-[190.5px] text-[40px] text-black text-center top-[345px] translate-x-[-50%] w-[111px]">
        <p className="leading-[1.35]">spark</p>
      </div>
      <div className="absolute bg-[50%_46.43%] bg-no-repeat bg-size-[100.86%_191.8%] h-[61px] left-[132px] top-[284px] w-[116px]" data-name="bafcd5e9-6f29-4a5f-a58a-dcf3eeab8c90 1" style={{ backgroundImage: `url('${imgBafcd5E96F294A5FA58ADcf3Eeab8C901}')` }} />
      <BottomButton />
      <BottomButton1 />
    </div>
  );
}